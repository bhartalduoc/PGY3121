function updateCharacterCount(element) {
    const maxLength = 150;
    const currentLength = element.value.length;
    const remainingCharacters = maxLength - currentLength;
    const counterElement = document.getElementById('contador-caracteres');
    counterElement.textContent = remainingCharacters + ' caracteres restantes';
  }