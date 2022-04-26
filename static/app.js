var form1 = true
var form2= false
var pathname = window.location.pathname;
console.log("________________", pathname)
function valitateForm1() {
     let id = document.forms["form"]["id-input"].value;
     let key = document.forms["form"]["key-input"].value;
     if (id.trim() == "" && key.trim() != ""){
       return "empty_id"
       }
     if (id.trim() != "" && key.trim() == ""){
       return "empty_key"
       }
    if (id.trim() == "" && key.trim() == ""){
       return "empty_both"
       }
    else
        return "pass"
}

function typing(field) {
    if (field == "id-input") {
      document.getElementById("id-input").style.borderColor = "gray";
      }
    if (field == "key-input") {
      document.getElementById("key-input").style.borderColor = "gray";
    }
}

function formOne() {
    let val = valitateForm1();
     if (val == "empty_id") {
      document.getElementById("id-input").style.borderColor = "red";
     } else if (val == "empty_key") {
      document.getElementById("key-input").style.borderColor = "red";
     }else if (val == "empty_both") {
      document.getElementById("id-input").style.borderColor = "red";
      document.getElementById("key-input").style.borderColor = "red";
     } else {
         se_id = document.getElementById("id-input").value
         document.getElementById("se_id").textContent = se_id
         api_key = document.getElementById("key-input").value
         document.getElementById("api_key").textContent = api_key

         
        document.getElementById("form1").style.display = "none";
        document.getElementById("form2").style.display = "block";
     }
}

function download_table_as_csv(table_id='customers', separator = ',') {
    // Select rows from table_id
    var rows = document.querySelectorAll('table#' + table_id + ' tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
            data = data.replace(/"/g, '""');
            // Push escaped string
            row.push('"' + data + '"');
        }
        csv.push(row.join(separator));
    }
    var csv_string = csv.join('\n');
    // Download it
    var filename = 'export_' + table_id + '_' + new Date().toLocaleDateString() + '.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
