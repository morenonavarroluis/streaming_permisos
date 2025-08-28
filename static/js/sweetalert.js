function confirmarEliminar(event, url) {
                                    event.preventDefault(); // Evita que el enlace navegue inmediatamente

                                    Swal.fire({
                                        title: '¿Estás seguro?',
                                        text: '¡No podrás revertir esto!',
                                        icon: 'warning',
                                        showCancelButton: true,
                                        confirmButtonColor: '#d33',
                                        cancelButtonColor: '#3085d6',
                                        confirmButtonText: 'Sí, ¡elimínalo!',
                                        cancelButtonText: 'Cancelar'
                                    }).then((result) => {
                                        if (result.isConfirmed) {
                                            window.location.href = url; // Redirige a la URL de eliminación si el usuario confirma
                                        }
                                    });
                                }