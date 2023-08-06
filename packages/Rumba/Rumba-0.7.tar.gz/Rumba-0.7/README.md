# Rumba: A framework to bootstrap a RINA network on a testbed

Rumba is a Python framework that allows users to write Python scripts
to define RINA networks and run scripted experiments. First, Rumba,
creates a physical network on one of the selected testbed. If needed,
Rumba can do an installation of the RINA prototype on the testbed
machines. The RINA network is then bootstrapped on the available
nodes. Finally, the experiment can be swapped out of the testbed.

Example scripts can be found in the examples/ folder.

## Workflow, both external and internal:

  1. Define the network graph, creating instances of model.Node and
     model.DIF classes.

  2. Create an instance of a Testbed class. See below for testbed
     specific configuration.

  3. Create an instance of the prototype.Experiment class, passing the
     testbed instance and a list of Node instances.

    1. At the end of the base Experiment constructor, the
       generate function is called to generate information about
       per-node IPCPs, registrations and enrollment, ready to be
       used by the plugins.

  4. Call methods on the prototype.Experiment instance:

    1. swap_in() swaps the experiment in on the testbed, and fills in
       the missing information in the model.

    2. install_prototype() installs the chosen prototype on the
       testbed. Currently an Ubuntu image is assumed.

    3. bootstrap_prototype() calls a prototype-specific setup function,
       to create the required IPCPs, perform registrations,
       enrollments, etc.

    4. swap_out() swaps the experiment out of the testbed.

## Installation

   For Debian and Ubuntu, the following command will ensure that the
   required dependencies are installed (replace python-dev with python3-dev
   if using Python 3):

      # apt-get install build-essential libssl-dev libffi-dev python-dev

   Rumba can be found on the
   [PyPi](https://pypi.python.org/pypi/Rumba) and can thus be
   installed through pip, by using `pip install rumba`.  To install
   the latest version, cloning the repository and install it from the
   command line:

      # python setup.py install

## Supported prototypes

 * [IRATI](https://github.com/IRATI/stack) is an open source
   implementation of the RINA architecture targeted at the OS/Linux
   system, initially developed by the FP7-IRATI project.

 * [rlite](https://github.com/vmaffione/rlite) is a lightweight Free
   and Open Source implementation of the Recursive InterNetwork
   Architecture (RINA) for GNU/Linux operating systems.

 * Ouroboros is a user-space implementation with a focus on
   portability. It is written in C89 and works on any POSIX.1-2001
   enabled system.

## Supported testbeds

 * [QEMU](http://wiki.qemu-project.org/Main_Page) is a generic and
   open source machine emulator and virtualizer.

   In order to use the qemu testbed, the user should install the
   qemu and bredge-utils packages ion which the testbed depends:

       # sudo apt-get install bridge-utils qemu

   A minimal QEMU testbed is defined as follows:

       tb = qemu.Testbed(exp_name = "twolayers",
                         username = "root",
                         password = "root")

   A user can optionally also specify the path to a bzImage and to an
   initramfs. If they are not specified, the latest buildroot image
   for the specific prototype will be downloaded. (Around 40 MB in
   size) The login to those images is root/root.

 * [Emulab](https://www.emulab.net/) is a network testbed, giving
   researchers a wide range of environments in which to develop,
   debug, and evaluate their systems.

   An emulab testbed instance is defined as follows:

       tb = emulab.Testbed(exp_name = "rochefort10",
                           username = "ricksanchez")

   A password can also be provided but is not necessary when an SSH
   key has been added. Optionally, a project name, a different testbed
   URL and a custom image can be specified.

   Issues have been reported that Rumba asks for the password even
   though a public key was added to the emulab interface. In this case
   a workaround is to start an ssh-agent and add the public key there.

       $ eval `ssh-agent`
       $ ssh-add /home/morty/.ssh/id_rsa.pub

 * [jFed](http://jfed.iminds.be/) is a Java-based framework for
   testbed federation.

   In order to use the jFed testbed, a user first needs to download
   his/her key from
   [https://authority.ilabt.iminds.be/](https://authority.ilabt.iminds.be/)
   After logging in, click on *Download your certificate*. Save the
   contents in a file (for example cert.pem). A jFed testbed instance
   is defined as follows:

       tb = jfed.Testbed(exp_name = "rochefort10",
                         username = "ricksanchez",
                         cert_file = "/home/morty/cert.pem")

   Here the experiment name is rochefort10, the user's name is
   ricksanchez, and the certificate can be found in
   /home/morty/cert.pem. An absolute path must be used for
   cert_file.

   To select a specific jFed testbed, set the authority parameter. The
   emulab and exogeni testbeds are stable and can be selected, for
   instance:

                         authority = "wall2.ilabt.iminds.be",

   or

                         authority = "exogeni.net",

   On the emulab testbeds, a specific machine image can be selected
   (set image_custom to True if you created a custom image):

                         image = "irati171031",
                         image_custom = True,

   Before running the rumba you must run an SSH agent in same terminal.
   This will also avoid you having to enter the passphrase for every
   login to a node by the framework if you are not on an IPv6 enabled network.
   (Apart from asking for the passphrase to login to the nodes, the framework
   will always ask for the passphrase since it is needed by the jFed
   CLI as well.) In order to start an SSH agent and to add the
   certificate, type the following commands:

       $ eval `ssh-agent`
       $ ssh-add /home/morty/cert.pem

   Pay attention to run your rumba script in the same terminal used
   for the previous commands, without changing the user (e.g. using su
   or sudo).

## Accessing nodes after swap-in

   To access a node once the experiment swapped in, use the following
   command (in the same terminal where ssh-agent was run in case of jFed):

       $ rumba-access $NODE_NAME

   Where $NODE_NAME is the name of the node to access. In case of the
   QEMU testbed, the password of the downloaded buildroot images is
   'root'.

## Acknowledgements

   Rumba is developed as part of the ARCFIRE project, funded by the
   European commission under the H2020 framework.