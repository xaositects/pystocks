SC={
    loadSectorPerformanceChart: function(){
        $.ajax({
            url:'/index.py/get_sector_perf_chart',
            success: function(d){
                $('#sec_perf').html(d);
            }
        });
    }
}
