<!DOCTYPE html>
<html>
<head>
    <title>Stock Advisor</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <script src="/js/jquery-1.11.1.min.js" type="text/javascript">
    </script>
    <script src="/js/materialize.js" type="text/javascript">
    </script>
    <script src="/js/Barchart.js" type="text/javascript">
    </script>
    <script src="/js/Chart.bundle.js" type="text/javascript">
    </script>
    <link rel="stylesheet" href="/css/materialize.css" type="text/css"/>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"/>
    <style type="text/css">
        a.btn {
            white-space: nowrap;
        }
    </style>

</head>
<body class="white">
<nav>
    <div class="nav-wrapper blue">
        <a href="#" class="brand-logo right"><i class="material-icons left">timeline</i>Stocks Advisor</a>
        {{ top_links }}
    </div>
</nav>
<h4>Portfolio: </h4>

<form method="post">
    <div class="container">
        {{portfolio}}

    </div>
    <div>{{positions}}</div>
    <h5>Add Symbols</h5>
    <label for='symbol'>Add Symbols (comma-separated)</label>
    <textarea name='symbol' id='symbol' class='materialize-textarea'></textarea>
    <button type="submit" class="btn blue black-text waves-effect" name="submit_symbol" value="Add">Add</button>
    <button type="submit" class="btn blue black-text waves-effect" name="reset_symbol" value="Set to Default">Set to
        Default
    </button>


</form>
</body>
</html>