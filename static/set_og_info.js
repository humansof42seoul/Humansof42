let title = document.getElementById('title').innerText;
document.title = title;
let og_image_tag = document.querySelector("meta[property='og:image']");
og_image_tag.setAttribute("content", "marie_gonzu");        
let og_title_tag = document.querySelector("meta[property='og:title']");
og_title_tag.setAttribute("content", "Humans of 42 | " + title);
