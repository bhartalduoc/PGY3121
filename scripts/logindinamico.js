function incrustarLogin() {
  // Obtén el elemento contenedor por su id
  var contenedor = document.getElementById("logindinamico");

  // Crea el código HTML del botón y el modal
  var codigoHTML = `
      <button type="button" class="btn btn-dark me-md-2" data-bs-toggle="modal" data-bs-target="#modalLogin">
        Iniciar sesión
      </button>
      
      <div class="modal fade" id="modalLogin" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="loginModalLabel">Inicio de sesión</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
            </div>

            <div class="modal-body">
              <form>
                <div class="btn-group btn-group-toggle w-100" data-toggle="buttons">
                  <label class="btn btn-light text-dark">
                    <input type="radio" name="perfil" id="administrador" autocomplete="off" checked> Administrador
                  </label>
                  <label class="btn btn-light text-dark">
                    <input type="radio" name="perfil" id="periodista" autocomplete="off"> Periodista
                  </label>
                </div>
              </form>

              <div class="modal-body">
                <form>
                  <div class="mb-3">
                    <label for="email" class="form-label">Correo electrónico</label>
                    <input type="plain" class="form-control" id="email" required>
                  </div>

                  <div class="mb-3">
                    <label for="password" class="form-label">Contraseña</label>
                    <input type="password" class="form-control" id="password" required>
                  </div>
                </form>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-dark" onclick="validarInicioSesion()">Iniciar Sesión</button>
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              </div>
            
          </div>
        </div>
      </div>
      `;

  // Inserta el código HTML en el contenedor al inicio
  contenedor.insertAdjacentHTML("afterbegin", codigoHTML);
}

function validarCorreoElectronico(email) {
  // Expresión regular para validar el formato del correo electrónico
  var regex = /^[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9]){1,}?$/;

  if (!regex.test(email)) {
    alert("El correo electrónico no es válido.");
    return false;
  }

  return true;
}

function validarInicioSesion() {
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  if (email === "") {
    alert("Por favor, ingrese su correo electrónico.");
    return;
  }

  if (!validarCorreoElectronico(email)) {
    return;
  }

  if (password === "") {
    alert("Por favor, ingrese su contraseña.");
    return;
  }

  // Aquí puedes realizar otras validaciones o enviar los datos a un servidor, etc.

  // Si las validaciones son exitosas, cierra el modal
  var modal = document.getElementById("modalLogin");
  var modalInstance = bootstrap.Modal.getInstance(modal);
  modalInstance.hide();
}

window.onload = function () {
  incrustarLogin();
};
