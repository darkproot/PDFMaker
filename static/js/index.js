const textarea = document.getElementById('text');
const font = document.getElementById('font-family');
const button = document.getElementById('btn');

const API = 'http://pdfmaker-bvjy.onrender.com'

button.addEventListener('click', post_data);

function post_data() {
    let data = {
        method: "POST",
        headers: {
            "Content-Type": "application/json" 
        },
        body: JSON.stringify({
            text: textarea.value,
            font: font.value
        })
    };

    fetch(API + '/generator', data)
        .then(res => res.json())
        .then(data => {
            if (data.name) {
                telechargerFichier(API + `/pdf/${data.name}`, data.name)
            }
        })
        .catch(err => console.error(err));
}

function telechargerFichier(url, nomFichier) {
    const lien = document.createElement('a');
    
    lien.href = url;
    lien.download = nomFichier;
    
    document.body.appendChild(lien);
    lien.click();
    
    document.body.removeChild(lien);
}