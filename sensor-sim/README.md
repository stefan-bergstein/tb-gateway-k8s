
python sensor-http.py --server http://tb-rest-tb-gateway.apps.ushift3.stormshift.coe.muc.redhat.com/my_devices --log-level DEBUG

podman build . -t tb-gw-sim:latest -f containerfile


