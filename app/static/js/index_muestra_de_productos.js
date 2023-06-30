let seleccion = document.getElementById("seleccion");
let imgSeleccionada = document.getElementById("imgSeleccionada");
let modeloSeleccionado = document.getElementById("modeloSeleccionado");
let descripSeleccionada = document.getElementById("descripSeleccionada");
let colorSeleccionado = document.getElementById("colorSeleccionado");
let precioSeleccionado = document.getElementById("precioSeleccionado");
let txtIDSeleccionado = document.getElementById("txtIDSeleccionado");

function cargar(nombre, descripcion, color, precio, txtID, imagen) {
    seleccion.style.display = "block";

    imgSeleccionada.src = imagen;
    modeloSeleccionado.textContent = nombre;
    descripSeleccionada.textContent = descripcion;
    colorSeleccionado.textContent = "- " + color + " -";
    precioSeleccionado.textContent = "$ " + precio;
    txtIDSeleccionado.value = txtID;
}
function cerrar() {
    seleccion.style.display = "none";
}

let imgOriginal = document.querySelector("#img-original");
let imgHover = document.querySelector("#img-hover");

imgOriginal.addEventListener("mouseover", mostrarImagenHover);
imgOriginal.addEventListener("mouseout", ocultarImagenHover);

function mostrarImagenHover() {
    imgOriginal.style.display = "none";
    imgHover.style.display = "block";
}
function ocultarImagenHover() {
    imgHover.style.display = "block";
    imgOriginal.style.display = "none";
}