package com.agendamento.repository;

import com.agendamento.model.Prestador;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PrestadorRepository extends JpaRepository<Prestador, Long> {
    
    List<Prestador> findByAtivoTrue();
    
    List<Prestador> findByEspecialidadeContainingIgnoreCase(String especialidade);
    
    Optional<Prestador> findByEmail(String email);
    
    List<Prestador> findByNomeContainingIgnoreCaseOrEspecialidadeContainingIgnoreCase(
        String nome, String especialidade);
}