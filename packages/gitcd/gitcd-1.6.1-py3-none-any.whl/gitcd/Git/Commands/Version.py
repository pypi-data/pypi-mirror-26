from gitcd.Git.Command import Command
import pkg_resources
import requests
import pip
from packaging import version
from gitcd.Exceptions import GitcdPyPiApiException


class Version(Command):

    packageUrl = 'https://pypi.org/pypi/gitcd/json'

    def update(self):
        pass

    def execute(self, branch: str):
        checkUpgrade = True
        local = self.getLocalVersion()
        try:
            pypi = self.getPypiVersion()
        except GitcdPyPiApiException as e:
            pypi = 'unknown'
            message = str(e)
            checkUpgrade = False

        self.interface.info('Local %s' % local)
        self.interface.info('PyPi %s' % pypi)

        if checkUpgrade is False:
            self.interface.error(message)
            return

        if version.parse(local) < version.parse(pypi):
            upgrade = self.interface.askFor(
                "Do you want me to upgrade gitcd for you?",
                ["yes", "no"],
                "yes"
            )
            if upgrade == 'yes':
                try:
                    pip.main(['install', '--user', 'gitcd', '--upgrade'])
                    return
                except SystemExit as e:
                    self.interface.error('An error occured during the update!')
                    pass

            self.interface.info(
                'Please upgrade by running pip3 install gitcd --upgrade'
            )
        else:
            self.interface.ok(
                'You seem to be on the most recent version, congrats'
            )

    def getLocalVersion(self):
        return pkg_resources.get_distribution("gitcd").version

    def getPypiVersion(self):
        response = requests.get(
            self.packageUrl
        )

        if response.status_code != 200:
            raise GitcdPyPiApiException(
                "Could not fetch version info on PyPi site." +
                "You need to check manually, sorry for that."
            )

        result = response.json()
        return result['info']['version']
