#!/bin/sh
ID_RSA=/var/lib/openshift/5562b947ecdd5ce939000038/app-deployments/id_rsa
exec /usr/bin/ssh -o StrictHostKeyChecking=no -i $ID_RSA "$@"
