function getHtml() {
    return document.documentElement.outerHTML;
}

function downloadFile(file_data) {
    const link = document.createElement("a");
    const file = new Blob([file_data], { type: 'text/plain' });
    link.href = URL.createObjectURL(file);
    link.download = "html_code_loader_output.html";
    link.click();
    URL.revokeObjectURL(link.href);
}

chrome.action.onClicked.addListener(async (tab) => {
    chrome.scripting.executeScript({
        target : {tabId : tab.id},
        func: getHtml,
    }, function (response) {
        var html_code = response[0].result;
        console.log("Got html code!");
        chrome.scripting.executeScript({
            target : {tabId : tab.id},
            func : downloadFile,
            args : [html_code]
        }, function(response) {
            console.log("Nice!");
            console.log(response);
        });
    });
});
