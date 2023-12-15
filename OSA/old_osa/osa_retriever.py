import threading
import pyvisa

class Ando(threading.Thread):
    def __init__(self, gpib_address):
        threading.Thread.__init__(self)
        self.gpib_address = gpib_address
        self.rm = pyvisa.ResourceManager()
        try:
            self.inst = self.rm.open_resource('GPIB0::' + str(gpib_address) + '::INSTR')
        except:
            self.inst = None
            print('Could not connect to GPIB address ' + str(gpib_address))
        self.inst.timeout = 10000
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'
        self._stop_event = threading.Event()
        self._stop_event.clear()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    # get the current trace
    def get_current_trace(self):
        try:
            trace = self.inst.query('ACTV?')
            if trace[0] == '2':
                return 'C'
            elif trace[0] == '1':
                return 'B'
            elif trace[0] == '0':
                return 'A'
            return
        except:
            print("Could not get current trace")

    # set the current trace
    def set_current_trace(self, trace):
        if trace == 'A':
            self.inst.write('ACTV0')
        elif trace == 'B':
            self.inst.write('ACTV1')
        elif trace == 'C':
            self.inst.write('ACTV2')
        return self.get_current_trace()

    # get display-status of current trace
    def get_display_status(self):
        try:
            status = self.inst.query('DSP' + self.get_current_trace() + '?')
            if status[0] == '1':
                return True
            elif status[0] == '0':
                return False
            return
        except:
            print("Could not get display status")

    def set_display_status(self, status):
        if status:
            self.inst.write('DSP' + self.get_current_trace())
        else:
            self.inst.write('DSP' + self.get_current_trace() + '0')
        return self.get_display_status()

    def retrieve_traces(self):
        print("Retrieving traces")
        try:
            # check which are set to display
            disp_a = self.inst.query('DSPA?')
            if disp_a[0] == '1': 
                disp_a = True
            else:
                disp_a = False
            disp_b = self.inst.query('DSPB?')
            if disp_b[0] == '1':
                disp_b = True
            else:
                disp_b = False
            disp_c = self.inst.query('DSPC?')
            if disp_c[0] == '1':
                disp_c = True
            else:
                disp_c = False

            if disp_a:
                trace_a = self.inst.query("LDATA")
                trace_a = trace_a.split(',')
                trace_a = trace_a[1:-1]
                trace_a = [float(x) for x in trace_a]
                lam_a = self.inst.query("WDATA")
                lam_a = lam_a.split(',')
                lam_a = lam_a[1:-1]
                lam_a = [float(x) for x in lam_a]
            if disp_b:
                trace_b = self.inst.query("LDATB")
                trace_b = trace_b.split(",")
                trace_b = trace_b[1:-1]
                trace_b = [float(x) for x in trace_b]
                lam_b = self.inst.query("WDATB")
                lam_b = lam_b.split(",")
                lam_b = lam_b[1:-1]
                lam_b = [float(x) for x in lam_b]
            if disp_c:
                trace_c = self.inst.query("LDATC")
                trace_c = trace_c.split(",")
                trace_c = trace_c[1:-1]
                trace_c = [float(x) for x in trace_c]
                lam_c = self.inst.query("WDATC")
                lam_c = lam_c.split(",")
                lam_c = lam_c[1:-1]
                lam_c = [float(x) for x in lam_c]

            # combine trace_a-lam_a, trace_b-lam_b, trace_c-lam_c into tuples of vectors to hold the returned parameters
            traces = []
            if disp_a:
                traces.append((trace_a, lam_a)) 
            if disp_b:
                traces.append((trace_b, lam_b))
            if disp_c:
                traces.append((trace_c, lam_c))
            return traces
        except Exception as e:
            print("Could not retrieve traces")
            print(e)
            return