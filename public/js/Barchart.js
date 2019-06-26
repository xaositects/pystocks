BC = {
    setOpinion: function(sym){
        $.ajax({
            url:'/index.py/get_current_opinion?sym=' + sym,
            success: function(d){
                $('#' + sym + '_opinion').html(d);
                $('#' + sym + '_opinion').append('<a href="https://www.barchart.com/stocks/quotes/' + sym + '/analyst-ratings" target="new"><i class="material-icons">link</i>');
            }
        });
    },
    loadOpinion: function (id, sym){
        this.setOpinion(sym);
    },
    loadOpinions: function(syms){
        for(let sym in syms){
            if(sym && sym !== 'None') {
                BC.loadOpinion(sym + '_opinion', sym);
            }
        }
    }
}