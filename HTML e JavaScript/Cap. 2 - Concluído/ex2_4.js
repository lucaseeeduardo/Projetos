// 1 - preciso pegar os dados do form e transformar numa variável

const frm = document.querySelector("form")
const resp1 = document.querySelector("h3") // aqui estou fazendo a resposta ser exibida na header 3

// 2 - preciso fazer referêcia do conteúdo inputado para as respostas nas headers

frm.addEventListener("submit", (e)=>{
    const preço = frm.inPreçoQuilo.value // a cada 1000g tenho x valor, portanto, é R$/1000g
    const consumo = frm.inConsumo.value // consumo em g
    const totalPagar = preço*consumo/1000// R$/1000g * g -- corta a unidade de grama e fica somente a unidade de preço R$ 
    resp1.innerText = `O total a pagar é de: R$ ${totalPagar.toFixed(2)}`

    e.preventDefault()

})