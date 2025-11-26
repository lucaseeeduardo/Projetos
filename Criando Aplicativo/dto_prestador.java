package com.agendamento.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PrestadorDTO {
    
    private Long id;
    
    @NotBlank(message = "Nome é obrigatório")
    private String nome;
    
    @NotBlank(message = "Especialidade é obrigatória")
    private String especialidade;
    
    @Email(message = "Email inválido")
    private String email;
    
    private String telefone;
    private String descricao;
    private Double precoHora;
    private Boolean ativo;
}