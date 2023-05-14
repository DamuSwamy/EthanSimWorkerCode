# Introduction 
This automation pack will allow to isolate/restore a Meraki Site-Site VPN connection for Pact Group. This will reduce the actual time taken to process the request from 15 minutes to a a maximum of 2 minutes depending on Meraki load. 

# Getting Started
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references


Installation Process:
st2 pack install https://ethangroup.visualstudio.com/SPBU%20Automation/_git/sim_meraki_pact

# Build and Test
Once the pack has been installed, navigate to the directory where the code has been cloned.
1. Navigate to sim_meraki_pact/actions/
2. sudo apt-get install python3-venv
3. Type in the following command: python3 -m venv venv
4. Type the next command to activate the virtual enviornment: source venv/bin/activate.
5. Once you have activated the virtual enviornment, type the following to install all requirements: pip install -r requirements.txt
6. Once all the requirements have been installed, create an enviornment variable " vi .env " . Enter the following information in the file.  api_key = "merakiapikeyfrompwdstate"
7. Save and exit the file.


# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
