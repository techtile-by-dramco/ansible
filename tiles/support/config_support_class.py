import yaml

''' Support class for reading and manipulating the techtile_devices.json 
    configuration file.
'''
class config_support_class:

    ''' Constructor
        configFile  filename of the json file that describes the techtile configuration
    '''
    def __init__(self, configFile: str):
        self.__configFile = configFile

        # Retrieve information about the Techtile setup
        with open(self.__configFile) as yaml_file:
            self.__techtileConfig = yaml.safe_load(yaml_file)


    ''' Return a tuple (midspanName, midspanIp, portNr) based on a given host
        If host is a group name, return a list of tuples
    '''
    def getMidspanInfo(self, host: str):
        hostList = self.__testIfGroup(host)

        result = []

        for h in hostList:
            # First look-up host information
            try:
                midspanName = self.__techtileConfig["all"]["hosts"][h]["midspan"]
                portNr = self.__techtileConfig["all"]["hosts"][h]["poe-port"]
            except KeyError:
                print('ERROR: Specified host "' + h + '" is not found in the "' + self.__configFile + '" file,')
                print('       OR it has an incomplete midspan configuration.')
                midspanName = ''
                portNr = ''

            if midspanName != '':
                # Now look-up midspanIp
                try:
                    midspanIp = self.__techtileConfig["all"]["vars"]["midspans"][midspanName]["ip"]
                    nrOfPorts = self.__techtileConfig["all"]["vars"]["midspans"][midspanName]["nr-ports"]
                except KeyError:
                    print('ERROR: midspan with name "' + midspanName + '" was specified for host "' + host + '"')
                    print('       in the "' + self.__configFile + '" file. However, configuration for this midspan is')
                    print('       missing in that same file.')
                    midspanIp = ''
                    nrOfPorts = 0

                # Final check
                if portNr > nrOfPorts:
                    print('ERROR: poe-port "' + str(portNr) + '" for the specified host "' + host + '" exceeds')
                    print('       the number of ports on the midspan ("' + midspanName +'")')
                    nrOfPorts = -1

                # Append retrieved info to the list
                result.append((h, midspanName, midspanIp, portNr))

        return result


    ''' Utility functions
    '''
    def __testIfGroup(self, host: str):
        if isinstance(host, list):
            return host

        # First look-up host information
        try:
            midspanName = self.__techtileConfig["all"]["hosts"][host]["midspan"]
            return [host]
        except KeyError:
            # if host not found -> check children first
            try:
                hostList = self.__techtileConfig["all"]["children"][host]["hosts"]
                return hostList.keys()
            except KeyError:
                print('ERROR: Specified host "' + host + '" not found in the "' + self.__configFile + '" file.')
                return []
