import ctypes
import xml.etree.ElementTree as ET

class WindowsLogs:
    def __init__(self) -> None:        
        self.wevtapi = ctypes.windll.wevtapi
        self.EVT_QUERY_CHANNEL_PATH = 1
        self.EVT_QUERY_FLAGS_FORWARD = 1
        self.EVT_HANDLE = ctypes.c_void_p
        self.EvtQuery = self.wevtapi.EvtQuery
        self.EvtQuery.restype = self.EVT_HANDLE
        self.EvtQuery.argtypes = [
            ctypes.c_wchar_p, 
            ctypes.c_wchar_p, 
            ctypes.c_wchar_p, 
            ctypes.c_ulong
        ]
        self.EvtNext = self.wevtapi.EvtNext
        self.EvtNext.restype = ctypes.c_bool
        self.EvtNext.argtypes = [
            self.EVT_HANDLE, 
            ctypes.c_ulong, 
            ctypes.POINTER(self.EVT_HANDLE), 
            ctypes.c_ulong, 
            ctypes.c_ulong, 
            ctypes.POINTER(ctypes.c_ulong)
        ]
        self.EvtRender = self.wevtapi.EvtRender
        self.EvtRender.restype = ctypes.c_ulong
        self.EvtRender.argtypes = [
            self.EVT_HANDLE, 
            self.EVT_HANDLE, 
            ctypes.c_ulong, 
            ctypes.c_ulong, 
            ctypes.c_void_p, 
            ctypes.POINTER(ctypes.c_ulong), 
            ctypes.POINTER(ctypes.c_ulong)
        ]
        self.EVT_RENDER_FLAGS_EVENT_XML = 1
    def xml_to_dict(self, xml_str):
        root = ET.fromstring(xml_str)
        def parse_element(element):
            parsed = {}
            if list(element):
                for child in element:
                    child_tag = child.tag
                    child_parsed = parse_element(child)
                    if child_tag not in parsed:
                        parsed[child_tag] = child_parsed
                    else:
                        if not isinstance(parsed[child_tag], list):
                            parsed[child_tag] = [parsed[child_tag]]
                        parsed[child_tag].append(child_parsed)
            else:
                parsed = element.text
            return parsed
        return {root.tag: parse_element(root)}
    def query_event_log(self, LogName ,xml_filter):
        event_log_handle = self.EvtQuery(None, LogName, xml_filter, self.EVT_QUERY_FLAGS_FORWARD)
        if not event_log_handle:
            raise ctypes.WinError()
        event_handles = (self.EVT_HANDLE * 1)()
        buffer_used = ctypes.c_ulong(0)
        property_count = ctypes.c_ulong(0)
        Eventsdata = []
        while self.wevtapi.EvtNext(event_log_handle, 1, event_handles, 0, 0, ctypes.byref(buffer_used)):
            buffer_size = ctypes.c_ulong(0)
            self.wevtapi.EvtRender(None, event_handles[0], self.EVT_RENDER_FLAGS_EVENT_XML, 0, None, ctypes.byref(buffer_size), ctypes.byref(property_count))
            if buffer_size.value > 0:
                buffer = ctypes.create_unicode_buffer(buffer_size.value)
                self.wevtapi.EvtRender(None, event_handles[0], self.EVT_RENDER_FLAGS_EVENT_XML, buffer_size.value, buffer, ctypes.byref(buffer_size), ctypes.byref(property_count))
                event_xml = buffer.value
                event_dict = self.xml_to_dict(event_xml)
                Eventsdata.append(event_dict)
        if len(Eventsdata)>0:
            return Eventsdata
        else:
            return "No data found"