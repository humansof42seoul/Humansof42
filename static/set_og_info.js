let title = document.getElementById('title').innerText;
document.title = title;
let thumbnail_url = document.querySelector('#main-img').dataset.thumbnail;
let og_image_tag = document.querySelector("meta[property='og:image']");
og_image_tag.setAttribute("content", thumbnail_url);        
let og_title_tag = document.querySelector("meta[property='og:title']");
og_title_tag.setAttribute("content", "Humans of 42 | " + title);
