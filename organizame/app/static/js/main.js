// Script principal para o Sistema de Prontuários UBS

document.addEventListener("DOMContentLoaded", function () {
  // Auto-fechar alertas após 5 segundos
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const closeButton = alert.querySelector(".btn-close");
      if (closeButton) {
        closeButton.click();
      }
    }, 5000);
  });

  // Formatar campos de telefone
  const telefoneInputs = document.querySelectorAll('input[name="telefone"]');
  telefoneInputs.forEach(function (input) {
    input.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length > 11) {
        value = value.substring(0, 11);
      }

      if (value.length > 7) {
        value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, "($1) $2-$3");
      } else if (value.length > 2) {
        value = value.replace(/^(\d{2})(\d{0,5})/, "($1) $2");
      }

      e.target.value = value;
    });
  });

  // Formatar campos de Cartão SUS
  const cartaoSusInputs = document.querySelectorAll('input[name="cartao_sus"]');
  cartaoSusInputs.forEach(function (input) {
    input.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length > 15) {
        value = value.substring(0, 15);
      }

      if (value.length > 0) {
        value = value.replace(
          /^(\d{3})(\d{0,4})(\d{0,4})(\d{0,4}).*/,
          function (match, p1, p2, p3, p4) {
            let result = p1;
            if (p2) result += " " + p2;
            if (p3) result += " " + p3;
            if (p4) result += " " + p4;
            return result;
          }
        );
      }

      e.target.value = value;
    });
  });

  // Confirmação para exclusão
  const deleteButtons = document.querySelectorAll(
    'button[type="submit"].btn-danger'
  );
  deleteButtons.forEach(function (button) {
    button.addEventListener("click", function (e) {
      if (
        !confirm(
          "Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita."
        )
      ) {
        e.preventDefault();
      }
    });
  });
});
