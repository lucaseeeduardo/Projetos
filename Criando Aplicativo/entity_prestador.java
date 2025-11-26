package com.agendamento.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "prestadores")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Prestador {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "Nome é obrigatório")
    @Column(nullable = false, length = 100)
    private String nome;
    
    @NotBlank(message = "Especialidade é obrigatória")
    @Column(nullable = false, length = 100)
    private String especialidade;
    
    @Email(message = "Email inválido")
    @Column(unique = true, length = 100)
    private String email;
    
    @Column(length = 20)
    private String telefone;
    
    @Column(length = 500)
    private String descricao;
    
    @Column(name = "preco_hora")
    private Double precoHora;
    
    @Column(name = "ativo")
    private Boolean ativo = true;
    
    @OneToMany(mappedBy = "prestador", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<HorarioDisponivel> horariosDisponiveis = new ArrayList<>();
    
    @OneToMany(mappedBy = "prestador", cascade = CascadeType.ALL)
    private List<Agendamento> agendamentos = new ArrayList<>();
}