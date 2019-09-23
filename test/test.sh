EDDIR=/mnt/PASSPORT/data/eap/energy-dashboard
LOGLEVEL=INFO
#LOGLEVEL=DEBUG
PREFIX="--log-level ${LOGLEVEL}"
TESTFEED="abc-test-01"
#set -x

runcmd(){
    echo "-------------------------------------------------"
    echo $1
    echo "-------------------------------------------------"
    $1
    if [ "$?" != "0" ]; then
        echo "TEST FAILED!!!"
        exit 1
    fi
    echo ""
    echo ""
}

runcmd_ignore_errors(){
    echo "-------------------------------------------------"
    echo $1
    echo "-------------------------------------------------"
    echo ""
    echo ""
}

./qtest.sh
runcmd_ignore_errors "edc ${PREFIX} feed ${TESTFEED} proc all"
runcmd "edc ${PREFIX} feed ${TESTFEED} s3urls"
runcmd "edc ${PREFIX} feed ${TESTFEED} proc dist"
runcmd "edc ${PREFIX} feed ${TESTFEED} s3archive"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"
# need the state files to use s3restore, so don't delete them
rm -rf ./data/${TESTFEED}/db/*.db
rm -rf ./data/${TESTFEED}/zip/*.zip
runcmd "edc ${PREFIX} feed ${TESTFEED} s3restore"
runcmd "edc ${PREFIX} feed ${TESTFEED} status --header"

echo "TEST PASSED"
