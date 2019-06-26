SC={
    getSectorPerformanceChart: function(id){
        $.post("https://stockcharts.com/freecharts/sectorsummary.html?O=4", function(data){
          var chart = $("#pagecontents .container", data); // finds <div id='mainDiv'>...</div>
        }, "html");
        $('#' + id).html(chart);
    }
}
