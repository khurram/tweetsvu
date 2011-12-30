google.load('visualization', '1.0', {'packages':['corechart']});
google.load('visualization', '1.0', {'packages':['gauge']});
  
google.setOnLoadCallback(drawTagChart);

function drawTagChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'hashtag');
  data.addColumn('number', 'Frequency');
  data.addRows([
    {% for tag in tag_count[:10]: %}
    ['{{ "#" + tag[0] }}', {{ tag[1] }}],
    {% endfor %}
  ]);

  var options = {
    width: 740, height: 500, fontSize: 16, 
    chartArea:{left: 120, top: 0, width: "100%", height: "100%"}
  };

  var chart = new google.visualization.BarChart(document.getElementById('tag_count'));
  chart.draw(data, options);

  google.visualization.events.addListener(chart, 'select', selectHandler)

  function selectHandler(e) {
    query = data.getValue(chart.getSelection()[0].row, 0).slice(1);
    window.location.replace("/search?q=%23" + query);
  }
}

google.setOnLoadCallback(drawUserChart);
function drawUserChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'hashtag');
  data.addColumn('number', 'Frequency');
  data.addRows([
    {% for user in user_count[:10]: %}
    ['{{ "#" + user[0] }}', {{ user[1] }}],
    {% endfor %}
  ]);

  var options = {
    width: 740, height: 500, fontSize: 16, 
    chartArea:{left: 120, top: 0, width: "100%", height: "100%"}
  };

  var chart = new google.visualization.BarChart(document.getElementById('user_count'));
  chart.draw(data, options);
}
  
google.setOnLoadCallback(drawGauge);
  
function drawGauge() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Label');
  data.addColumn('number', 'Value');
  data.addRows([
    ['Sentiment', {{ sentiment }}]
  ]);

  var options = {
    width: 200, height: 200, redFrom: 0, redTo: 40, minorTicks: 5,
    yellowFrom: 40, yellowTo: 60, greenFrom: 60, greenTo: 100
  };

  var chart = new google.visualization.Gauge(document.getElementById('sentiment'));
  chart.draw(data, options);
}

google.setOnLoadCallback(drawArea);

function drawArea() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Date');
  data.addColumn('number', 'Sentiment');
  data.addRows([
    {% for tweet in tweets: %}
    ['{{ tweet['created_at']|time_since }}', {{ tweet['polarity'] }}],
    {% endfor %}
  ]);

  var options = {
    width: 540, height: 300,
    title: 'Tweet Activity', isStacked: true,
    vAxis: {title: 'Negative <--> Positive',  titleTextStyle: {color: 'red'}},
    chartArea:{left: 80, top: 10, width: "100%", height: "75%"}
  };

  var chart = new google.visualization.AreaChart(document.getElementById('sentiment_graph'));
    chart.draw(data, options);
}
