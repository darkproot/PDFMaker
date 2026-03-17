const textarea = document.getElementById('text');
const font = document.getElementById('font-family');
const button = document.getElementById('btn');
const output_name = document.getElementById('output-name');

const API = 'https://pdfmaker-bvjy.onrender.com'
// const API = 'http://localhost:8888'

// button.addEventListener('submit', (e) => post_data(e));

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
                telechargerFichier(API + `/pdf/${data.name}`, output_name.value)
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