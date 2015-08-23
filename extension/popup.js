chrome.tabs.getSelected(null, function(tab) {
    document.body.style.backgroundColor="#EEE6D4"
    document.body.style.color="#2F6015"
    var server_url = 'http://ec2-52-68-41-17.ap-northeast-1.compute.amazonaws.com:5000/?url=';
    document.getElementById('currentTitle').innerHTML = tab.title;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", server_url + tab.url, true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        // Show keywords
        document.getElementById("keywords").innerHTML = '';
        var keywords = JSON.parse(xhr.responseText).keywords;
        keywords.forEach(function(keyword) {
          var word = document.createElement("a");
          word.appendChild(document.createTextNode(keyword + '       '));
          document.getElementById("keywords").appendChild(word);
        });
        // Show articles
        document.getElementById("articles").innerHTML = '';
        var articles = JSON.parse(xhr.responseText).articles;
        articles.forEach(function(article) {
          var score = Math.round(article.score * 100) / 100;
          var link = document.createElement("a");
          link.setAttribute('href', article.url);
          link.appendChild(document.createTextNode('('+score+') '+article.title));
          link.style.fontSize = 8 + (Math.round(article.score * 100)/3) + 'px';
          document.getElementById("articles").appendChild(link);
          // Space
          var space = document.createElement("br");
          document.getElementById("articles").appendChild(space);
        });
      }
    }
    xhr.send();
});
