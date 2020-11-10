#!/bin/bash

ls Initial.ldif

kubectl cp Initial.ldif auth/$(kubectl get pods -n auth | grep -i ldap | awk '{print $1}'):.

kubectl -n auth exec -it $(kubectl get pods -n auth | grep -i ldap | awk '{print $1}')  -- bash

# Inside Pod
ldapadd -x -W -H ldap://ldap-openldap.auth.svc.cluster.local:389 -D "cn=admin,dc=jupyterbook,dc=com" -f Initial.ldif