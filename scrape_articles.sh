
if [ $# -lt 1 ]; then
    echo "Error, need to specify port..."
    exit 1
fi

PORT=$1

URLS="http://www.nytimes.com/2013/05/29/business/energy-environment/solar-powers-dark-side.html?hp
http://www.washingtonpost.com/local/nearly-40-percent-of-mothers-are-now-the-family-breadwinners-report-says/2013/05/28/8de03ec8-c7bb-11e2-9245-773c0123c027_story.html?hpid=z1"

for url in `echo $URLS`
do
    echo "Curling ${url}"
    curl -d url=$url http://localhost:$PORT/jobs/crawler/scrape_article
    echo
done
