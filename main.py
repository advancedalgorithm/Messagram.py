import requests, subprocess, socket, threading, time

from user import *
from response import *

MAX_BYTE = 1024

class Messagram():
    """
     *        The Official Messagram Client Library
     * 
     * Quick Start Example:
     * 
     * Form Open:
     * 
     *     - Set a Messagram Property For The Main Client Form
     *     - Add a Messagram Function Argument to the Form's Constructor
     *     
     *          m = Messagram("CLIENT_NAME", "CLIENT_VERSION");
     *          
     * Upon Login: 
     *          
     *          messaResponse r = m.ConnectnAuthorize(textBox1.Text, textBox2.Text);
     *          if (r.resp_t != Resp_T.SOCKET_CONNECTED)
     *          {
     *              MessageBox.Show("Messagram server is down!");
     *              Environment.Exit(0);
     *          } else if(r.cmd == Cmd_T.SUCCESSFUL_LOGIN)
     *          {
     *              MessageBox.Show($"Welcome {username} to Messagram!");
     *              ClientForm c = new ClientForm(m) // YOUR CLIENT FORM HERE
     *              this.close();
     *              c.ShowDialog();
     *          }
    """

    
    """ Client Application Information """
    client_name         : str = "official_messagram_client_v.0.0.1";
    client_version      : str = "0.0.1";

    """ Client's Current User Information """
    Username            : str;
    sessionID           : str;
    hwid                : str;
    acc_info            : dict[str, str];

    """ Client's Current Opened Chat """
    listen_to_chat      : str;
    listen_to           : str;
    currentChat_T       : Message_T;
    currentChats        : Message;

    """ Client's Current Opened Chat """
    chat_opened         : str; # this must be enabled in-order to 
    dm                  : bool; # dm on true, community chat on false
    chat_name           : str; # chat_name to listen to
    
    """ Messagram Server Information & Connections """
    _BACKEND            : str = "195.133.52.252";
    _BACKEND_PORT       : str = 666;
    server              : socket.socket;
    terminate           : bool = False;
    DMs                 : list[DM];
    Communities         : list[Community]
    ServerLogs          : str;
    def __init__(self, n: str, v: str):
        self.ServerLogs = ""
        self.Messages = []
        self.client_name = n;
        self.client_version = v;
        self.retrieveHardwareInfo();

    def retrieveHardwareInfo(self) -> None:
        try:
            self.hwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        except: self.hwid = subprocess.getoutput('cat /var/lib/dbus/machine-id')

    # def setNewChat(self, listen: str, chat_t: Message_T, messages):


    def ConnectnAuthorize(self, username: str, password: str) -> Response:
        self.sessionID = requests.get(f"https://api.yomarket.info/auth?username={username}&password={password}&hwid={self.hwid}").text

        if self.sessionID == "":
            return Response("Unable to retrieve Hardware ID to continue", True, Resp_T.NULL, Cmd_T.invalid_parameters)
        
        if self.sessionID == "[ X ] Error, Unable to find account...!":
            return Response("Unable to find account!", True, Resp_T.NULL, Cmd_T.invalid_login_info)
        
        """ Connecting to Messagram Server and Handling Request """
        try: self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err: return Response("Invalid Connection", False, Resp_T.socket_rejected)
        except: return Response("Invalid Connection", False, Resp_T.invalid_connection)
        self.server.connect((self._BACKEND, self._BACKEND_PORT))

        self.Username = username
        self.acc_info = {"username": self.Username, 
                         "sid": self.sessionID, 
                         "hwid": self.hwid, 
                         "client_name": self.client_name, 
                         "client_version": self.client_version
        }

        new_r = self.SendCmd(Cmd_T.client_authentication, {})

        gg = threading.Thread(target=self.Listener)
        gg.start()

        return new_r
    
    def Listener(self) -> None:
        try:
            while True:
                print("[ + ] Listening")
                data = self.server.recv(MAX_BYTE).decode().strip()
                self.ServerLogs += f"{data}\n"

                r = Response(data.replace("'", "\"").replace(":", ": "), False)

                match r.resp_t:
                    case Resp_T.user_resp:
                        n = self.buildOutput(f"[{r.resp_t}|{r.cmd_t}] Error, Invalid Operation!", r.resp_t, r.cmd_t)
                        self.Messages.append(Message(Message_T.DM if "to_username" in r.server_resp else Message_T.COMMUNITY,
                                                    r.from_username,
                                                    r.server_resp['to_username'],
                                                    r.server_resp['data']))
                    case Resp_T.push_event:
                        continue
                    case Resp_T.mass_event:
                        # RECEIVED A MASS EVENT
                        continue
        except Exception as e:
            print(f"[ X ] Error, Messagram Disconnect | A socket error has occured....!\n\n{e}")
            return

    def buildOutput(self, d: str, r: Resp_T, c: Cmd_T) -> Response:
        return Response(d, False, r, c)

    # Choose a command type and provide the parameters, the rest of the JSON data is generated
    def SendCmd(self, c: Cmd_T, parameters: dict[str, str]) -> Response:
        new__ = Response("", True, Resp_T.NULL, c, self.acc_info, parameters)
        print(f"[ + ] Sending {new__.new_cmd}")
        
        self.server.send(f"{new__.new_cmd}\n".replace("'", "\"").encode())
        
        """
            Check for any other resp_t rather than user_resp
        """
        # IF A DM,Community_Chat gets caught in here send it elsewhere and wait for response again.
        # if new_cmd.resp_t != Resp_T.user_resp: 
            # send to handle elsewhere
        
        # data = self.server.recv(1024).decode().strip()
        # return Response(data, False)


m = Messagram("TEST_C", "TEST_V") # Set client information
gg = m.ConnectnAuthorize("vibe", "gay123") # Start Messagram Event Handler


""" Send a command to MessagramServer """
# m.SendCmd(Cmd_T.send_dm_msg, {"from_username": "vibe", "to_username": "Jeff", "data": "Hi, Im Vibe. im sending message to Jeff from a Messagram Python Client"})

# Start your own listener for messages
last_log_count = 0
time.sleep(1)
while True:
    if last_log_count < len(m.ServerLogs):
        print(m.ServerLogs[len(m.ServerLogs)-1])
    print(f"[ + ] Listening {len(m.Messages)} || {m.ServerLogs}")
    time.sleep(1000);