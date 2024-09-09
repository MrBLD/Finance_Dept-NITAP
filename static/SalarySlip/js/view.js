document.addEventListener("DOMContentLoaded", function () {
    const ExcelButton = document.querySelectorAll(".generateExcelButton");

    ExcelButton.forEach((button) => {
        button.addEventListener('click', function(){
            var month = this.dataset.month;
            var year = this.dataset.year;
           const url = `/excel/&{month}/&{year}/`;
            fetch(url, {
                method: "GET",
                success: function(data) {
                    console.log("Excel file generated successfully.");
                },
                error: function(error) {
                    console.error("Error generating Excel file:", error);
                }
            });
        })
    })
});