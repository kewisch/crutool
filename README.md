Welcome to crutool
==================
This tool allows simple interaction with JIRA and Crucible.

It has been tested with Crucible 2.7.4 and JIRA 4.4.1. There are known issues
with later versions. If you want to add support, please abstract the api and
response objects so that multiple versions can be supported.

Installing the keyring and GitPython module is highly recommended, it is not
required though. Mandatory reqirement is the iniparse module.The keyring module
will save your smtp/jira/fisheye password to the system keyring.

Usage
=====

In most commands, you can use the underscore _ to expand the last referenced
issue. For example:

    crutool review set CTL-1234
    crutool review _ show

Review (Crucible) Module
------------------------
    # Show information about the review
    crutool review <issue_or_cr> show
    crutool review <issue_or_cr>

    # Create a review with the review create command. You can supply all
    # parameters like so:
    crutool review create <project> <issue> <reponame> <changeset> [changeset...]
    
    # If you have GitPython installed you can rely on git to get the
    # information. Specify a project and a target branch to compare to:
    crutool review create <project> <targetbranch>

    # Going a step further, you can set the project key in the defaults section
    # of your configuration, then you only need to specify the target branch
    crutool review create <targetbranch>

    # Set the review status.
    # Valid status values are:
    #   summarize, close, reopen, complete,
    #   uncomplete, abandon, delete
    # You can summarize and close at once by using "close"
    crutool review <issue_or_cr> set <status>

    # Send a pullrequest email. If git support is not installed, revision
    # information will be taken from the review and if not specified the branch
    # name will be the issue id. This may be more than you want, especially if
    # you have rebased. Git support is highly recommended.  With git support,
    # revision information and branch (if not specified) is taken from 'git
    # cherry' and the active branch. Be sure to set up the [smtp] section of
    # your config file.
    crutool review <issue_or_cr> pr <targetbranch> [branch]

Jira Module
-----------
    # Show information about the issue
    crutool jira <issue> show
    crutool jira <issue>

    # Show possible status transitions for the issue
    crutool jira <issue> transitions

    # Set jira issue status. You will be interactively prompted for the target
    # state.
    crutool jira <issue> set

    # Show bugs assigned to you and open, by priority. Adding "all" shows all
    # summaries, but is slower. Without "all", only first summary is shown.
    crutool jira todo [all]

Other Commands
--------------

    # Clear authentication token from the keyring, if installed
    crutool authclear

    # Make a direct API call, useful for debugging
    crutool api <jira|cru> <http_method> <url> [header=value...]

    # Print the last referenced issue
    crutool _

Typical Workflow
================

First of all, create the issue via web interface. Unfortunately this is not
possible with the Jira 4.x REST API. For sake of argument, 'next' is the branch
the feature is heading for.

    crutool jira CTL-1234 set # Select 'Start Progress'
    git checkout next
    git checkout -b `crutool _`

Now fix your bugs. All of them.

    git commit -m "CTL-1234 - Fix it"
    git push myremote `crutool _`
    crutool review create CR next

Wait for your team to review the code. Then check if there are comments:

    crutool review _ show

Now fix the review comments, then commit.

    git commit -m "CTL-1234 - Whitespace fix"
    git push myremote `crutool _`
    crutool review _ add next # TODO Not yet implemented

You are done with the review. Summarize and close it:

    crutool review _ set close

Finally, rebase your changes and send a pull request via email:
    git rebase -i next
    crutool review  _ pr

Configuration
=============

Configuration on UNIX systems is saved in the ~/.crutoolrc file. On Windows,
use crutool.ini in your home directory.

    [defaults]
    project=CR                                  # The default project key, optional
    cru_base=https://localhost/fisheye          # Path to where your fisheye instance resides
    jira_base=https://localhost/jira            # Path to where your jira instance resides

    [smtp]
    smtp.from=John Doe <john@example.com>       # Email sender
    smtp.recipients=Dev Team <dev@example.com>  # Comma separated list of recipients
    smtp.host=mail.example.com                  # Email server to use
    smtp.username=john                          # Email server username
    smtp.ssl=True                               # Use SSL (Port 465) to connect (True|False)

    [templates]
    issue=This is the template for displaying issues.
       It can be multiline, as long as the second

       and following lines are indented. Empty lines
       are permitted.

    review=This is the template for displaying reviews
    pullrequest=This is the email template for pull requests


git integration
---------------

If you use git alot, you might find yourself typing "git jira" even though you meant "crutool jira". Its easy to integrate crutool with git using aliases. Put this in your ~/.gitconfig:

    [alias]
    jira = !crutool jira
    review = !crutool review

Then you can use git like this:

    git jira CTL-1234 show
    git review create CR next

Installation
============

crutool uses the standard setuptools shim, so all you have to do is clone the repository and type:
    
    sudo python setup.py install

afterwards, the crutool command will be available in your path.

License
=======

This work is distributed under the terms of the [Mozilla Public
License](http://www.mozilla.org/MPL/2.0/), because that is what I am used to.
