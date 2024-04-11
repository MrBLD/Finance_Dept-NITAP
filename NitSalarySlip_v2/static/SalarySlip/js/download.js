function manipulateData(data) {
    var mid = Math.ceil(data.length / 2);
    var part1 = data.slice(0, mid);
    var part2 = data.slice(mid);
    var table = document.getElementById("myTable");

    for (var i = 0; i < Math.max(part1.length, part2.length); i++) {
        var row = table.insertRow(table.rows.length);
        var cell1 = row.insertCell(0);
        cell1.innerHTML = i + 1;
        var cell2 = row.insertCell(1);
        cell2.innerHTML = i < part1.length ? part1[i] : '';
        var cell3 = row.insertCell(2);
        cell3.innerHTML = i < part2.length ? part2[i] : '';
    }
}
