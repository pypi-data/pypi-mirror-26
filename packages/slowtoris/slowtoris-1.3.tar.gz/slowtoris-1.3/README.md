# SlowToris

A Slow Loris attack implementation in Python3 with support for the Tor network and SOCKS5 proxies.

You can view the usage of this script by running:

    $ slowtoris.py --help
### Installing Slowtoris:

##### Using pip:

    $ pip install slowtoris

If you choose this solution you can jump to the Tor installation part.

##### Manually:

You must clone the git:

    $ git clone https://github.com/naganori-san/slowtoris

Move to the directory:

    $ cd slowtoris

Install the script:

    $ sudo python3 setup.py install

You must have the `click` Python3 module which can be installed with pip:

    $ sudo pip3 install click

You must have the socks Python3 module which can be installed through
various packages by using pip, we suggest `PySocks`:

    $ sudo pip3 install PySocks

If you wish to use the Tor network, tor must be installed.

### Installing Tor:

    Ubuntu/Debian:  https://www.torproject.org/docs/debian.html.en

    Arch Linux:     # pacman -S tor

    Gentoo Linux:   # emerge --ask --verbose net-vpn/tor

    CentOS/Fedora:  # yum install tor

### Usage:

    slowtoris.py [OPTIONS] TARGET

### Options:

  Options:

    -p, --port INTEGER           Port to attack on the remote target. Default is

                                 80.

    -s, --sockets INTEGER        Number of sockets to open with the remote

                                 target.

    -r, --randomize              Randomize user agents for every new socket.

    -t, --tor                    Open the connections through the Tor network.

                                 Jus to be safe you might want to run this as

                                 root if you are using Tor.

    -T, --tor_instances INTEGER  Number of Tor instances to start in rder to

                                 route the traffic through different circuits

                                 (default is 13).

    -x, --proxy HOST:PORT        Usage: -x proxy-host:proxy-port .Use a SOCKS5

                                 proxy to communicate with the target.

    -q, --quiet                  Run the script in quiet mode removing all

                                 output.

    --help                       Show this message and exit.
