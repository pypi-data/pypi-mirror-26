from gitcd.Git.Command import Command


class Clean(Command):

    def execute(self, dummy: str):
        self.update()
        origin = self.getOrigin()
        self.quietCli.execute("git remote prune %s" % origin)

        localTags = self.getLocalTags()
        remoteTags = self.getRemoteTags(origin)

        localBranches = self.getLocalBranches()
        remoteBranches = self.getRemoteBranches(origin)

        for branch in localBranches:
            if branch not in remoteBranches:
                if self.getCurrentBranch() == branch:
                    self.quietCli.execute(
                        "git checkout %s" %
                        self.config.getMaster())
                self.cli.execute("git branch -D %s" % branch)

        for tag in localTags:
            if tag not in remoteTags:
                self.cli.execute("git tag -d %s" % tag)
