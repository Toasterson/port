from git import Repo

# repo = Repo.clone_from('https://github.com/Toasterson/port.git', '~/.ports/tmp/git-test')
repo = Repo('~/.ports/tmp/git-test')
repo.remote('origin').pull()
git = repo.git
git.checkout('HEAD')
print(repo.index)
