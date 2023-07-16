// 1 - preciso criar uma variável que me dê acesso ao que existe no form
const frm = document.querySelector("form") // acessando o  local do form
const resp = document.querySelector("h3") // acessando o local da header 3

// 2 - acessados os locais necessários, agora preciso trabalhar com o conteúdo nesses locais
frm.addEventListener("submit", (e)=>{
    const nome = frm.inMedicamento.value
    const preço = Math.floor(2*(frm.inPreço.value))
    resp.innerText = `Promoção de ${nome}\n Leve 2 caixas por apenas: R$ ${preço.toFixed(2)}`
    e.preventDefault()
})