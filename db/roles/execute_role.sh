dbname=postgres
while getopts f:d: flag
do
    case "${flag}" in
        f) filename=${OPTARG};;
        d) dbname=${OPTARG};;
    esac
done

export PGPASSWORD=$KS_PG_PASSWORD
envsubst < $filename | psql -h localhost -p 5432 -U postgres -d $dbname
