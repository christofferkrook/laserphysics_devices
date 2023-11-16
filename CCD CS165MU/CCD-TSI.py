from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK
import time
import matplotlib.pyplot as plt
import os 
import csv
import tkinter as tk
from PIL import Image, ImageTk
import threading
import queue


class LiveViewCanvas(tk.Canvas):

    def __init__(self, parent, image_queue):
        ## type: (typing.Any, queue.Queue) -> LiveViewCanvas
        self.image_queue = image_queue
        self._image_width = 0
        self._image_height = 0
        tk.Canvas.__init__(self, parent)
        self.pack()
        self._get_image()

    def _get_image(self):
        try:
            image = self.image_queue.get_nowait()
            self._image = ImageTk.PhotoImage(master=self, image=image)
            if (self._image.width() != self._image_width) or (self._image.height() != self._image_height):
                # resize the canvas to match the new image size
                self._image_width = self._image.width()
                self._image_height = self._image.height()
                self.config(width=self._image_width, height=self._image_height)
            self.create_image(0, 0, image=self._image, anchor='nw')
        except queue.Empty:
            pass
        self.after(10, self._get_image)


class ImageAcquisitionThread(threading.Thread):

    def __init__(self, camera):
        # type: (TLCamera) -> ImageAcquisitionThread
        super(ImageAcquisitionThread, self).__init__()
        self._camera = camera
        self._previous_timestamp = 0

        # setup color processing if necessary
        if self._camera.camera_sensor_type != SENSOR_TYPE.BAYER:
            # Sensor type is not compatible with the color processing library
            self._is_color = False
        else:
            self._mono_to_color_sdk = MonoToColorProcessorSDK()
            self._image_width = self._camera.image_width_pixels
            self._image_height = self._camera.image_height_pixels
            self._mono_to_color_processor = self._mono_to_color_sdk.create_mono_to_color_processor(
                SENSOR_TYPE.BAYER,
                self._camera.color_filter_array_phase,
                self._camera.get_color_correction_matrix(),
                self._camera.get_default_white_balance_matrix(),
                self._camera.bit_depth
            )
            self._is_color = True

        self._bit_depth = camera.bit_depth
        self._camera.image_poll_timeout_ms = 0  # Do not want to block for long periods of time
        self._image_queue = queue.Queue(maxsize=2)
        self._stop_event = threading.Event()

    def get_output_queue(self):
        # type: (type(None)) -> queue.Queue
        return self._image_queue

    def stop(self):
        self._stop_event.set()

    def _get_color_image(self, frame):
        # type: (Frame) -> Image
        # verify the image size
        width = frame.image_buffer.shape[1]
        height = frame.image_buffer.shape[0]
        if (width != self._image_width) or (height != self._image_height):
            self._image_width = width
            self._image_height = height
            print("Image dimension change detected, image acquisition thread was updated")
        # color the image. transform_to_24 will scale to 8 bits per channel
        color_image_data = self._mono_to_color_processor.transform_to_24(frame.image_buffer,
                                                                         self._image_width,
                                                                         self._image_height)
        color_image_data = color_image_data.reshape(self._image_height, self._image_width, 3)
        # return PIL Image object
        return Image.fromarray(color_image_data, mode='RGB')

    def _get_image(self, frame):
        # type: (Frame) -> Image
        # no coloring, just scale down image to 8 bpp and place into PIL Image object
        scaled_image = frame.image_buffer >> (self._bit_depth - 8)
        return Image.fromarray(scaled_image)

    def run(self):
        while not self._stop_event.is_set():
            try:
                frame = self._camera.get_pending_frame_or_null()
                if frame is not None:
                    if self._is_color:
                        pil_image = self._get_color_image(frame)
                    else:
                        pil_image = self._get_image(frame)
                    self._image_queue.put_nowait(pil_image)
            except queue.Full:
                # No point in keeping this image around when the queue is full, let's skip to the next one
                pass
            except Exception as error:
                print("Encountered error: {error}, image acquisition will stop.".format(error=error))
                break
        print("Image acquisition has stopped")
        if self._is_color:
            self._mono_to_color_processor.dispose()
            self._mono_to_color_sdk.dispose()


class CameraController:
    def __init__(self):
        self.save_dir = os.getcwd() + "/TSI-images"
        r = os.path.isdir(self.save_dir)
        if r == False:
            os.mkdir(self.save_dir)
        sdk = TLCameraSDK()
        print("Welcome to Thorlabs Scientific Imaging program")

        try:
            camera_list = sdk.discover_available_cameras()
            print("Detected the following cameras:")
            for i, camera in enumerate(camera_list):
                print("Camera number " + str(i) + "     - Serialnumber " + camera)
        except:
            print("Could not find camera. Did you open the port? try sudo chmod 666 /dev/video0 /dev/video1 /dev/input//event7")

        cam_nr = input("Which camera would you like to open? : ")

        #  Open the camera
        try:
            self.cam = sdk.open_camera(camera_list[int(cam_nr)])
            self.cam.frames_per_trigger_zero_for_unlimited = 0
            self.cam.arm(2)
            self.cam.issue_software_trigger()
            self.cam.image_poll_timeout_ms = 0 
            time.sleep(1)
            print("Opened camera " + camera)
        except:
            print("Could not open camera " + camera)

        print("The current settings of the camera is : ")
        print("   - Exposure time : " + str(self.cam.exposure_time_us) + " µs. Valid range is " + str(self.cam.exposure_time_range_us))
        print("   - Gain : " + str(self.cam.gain) + ". Valid range is " + str(self.cam.gain_range))
        self.main_loop()

    def print_commands(self):
        print("\nAvailable commands: ")
        print("   - changegain. Changes the gain")
        print("   - exposuretime. Changes the exposure time")
        print("   - retrieveimage. Retrieves an image from the camera")
        print("   - live. Starts live view of the camera")
        print("   - commands. Displays the available commands again")
        print("   - quit. Closes connection (if opened) and quits the program")

    def main_loop(self):
        self.print_commands()

        while True:
            command = input(" - Command: ")

            if command == "changegain":
                gain = input("   - Gain: ")
                try:
                    self.cam.gain = int(gain)
                except:
                    print("Could not change gain to " + gain)
                ga = self.cam.gain
                print("Gain changed to " + str(ga))
            
            if command == "exposuretime":
                exposure_time = input("   - Exposure time (The camera will round it a bit) (µs): ")
                try:
                    self.cam.exposure_time_us = int(exposure_time)
                except:
                    print("Could not change exposure time to " + exposure_time)
                et = self.cam.exposure_time_us
                print("Exposure time changed to " + str(et) + " µs")

            if command == "retrieveimage":
                print("Retrieving image")
                frame = self.cam.get_pending_frame_or_null()
                if frame is not None:
                    print("Image retrieved")
                    print("   - Image width: " + str(frame.image_buffer.shape[1]))
                    print("   - Image height: " + str(frame.image_buffer.shape[0]))
                    print("   - Image size: " + str(frame.image_buffer.size))
                    image = frame.image_buffer << (self.cam.bit_depth - 8)

                    plt.imshow(image, cmap='gray')
                    plt.show()
                    plt.draw()

                    r = input("Do you want to save this image to a file? y/n: ")
                    if r == 'y':
                        file_name = input("   - File name (no extension): ")
                        # open the file in the write mode
                        f = open(self.save_dir + "/" + file_name + ".csv", 'w')
                        # create the csv writer
                        writer = csv.writer(f)
                        for row in image:
                            # write a row to the csv file
                            writer.writerow(row)
                        # close the file
                        f.close()

                else:
                    print("Could not retrieve image")

            if command == "live":
                self.show_live_view()

            if command == "quit":
                print("Closing connection to camera")
                self.cam.disarm()
                self.cam.dispose()
                break
        print("Exiting program")

    def get_live_image(self):
        frame = None
        while frame == None:
            frame = self.cam.get_pending_frame_or_null()
            if frame is None:
                print("Frame is none")
            else:
                return frame.image_buffer << (self.cam.bit_depth - 8)

    def show_live_view(self):
        # create generic Tk App with just a LiveViewCanvas widget
            print("Generating app...")
            root = tk.Tk()
            root.title(self.cam.name)
            image_acquisition_thread = ImageAcquisitionThread(self.cam)
            camera_widget = LiveViewCanvas(parent=root, image_queue=image_acquisition_thread.get_output_queue())

            print("Starting image acquisition thread...")
            image_acquisition_thread.start()

            print("App starting")
            root.mainloop()

            print("Waiting for image acquisition thread to finish...")
            image_acquisition_thread.stop()
            image_acquisition_thread.join()


# Instantiate the camera controller
controller = CameraController()