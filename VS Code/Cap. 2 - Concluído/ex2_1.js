// criando referência ao form e ao elemento h3, onde será exibida a resposta.
const frm = document.querySelector("form") // que que ta acontecendo?
const resp = document.querySelector("h3") // o que corre aqui?
// agora eu crio um "ouvinte" do evento (como assim ouvinte?), acionando quando o botão submit for clicado
frm.addEventListener("submit", (e) => {
    const nome = frm.inNome.value // aqui pegou o nome do form - como assim pegou?
    resp.innerText = `Olá ${nome}` // aqui printa -- o que tá acontecendo aqui?
    e.preventDefault() // evita envio do form ??? o que significa isso?
})
