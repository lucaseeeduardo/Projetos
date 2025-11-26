package com.agendamento.service;

import com.agendamento.dto.PrestadorDTO;
import com.agendamento.model.Prestador;
import com.agendamento.repository.PrestadorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class PrestadorService {
    
    @Autowired
    private PrestadorRepository prestadorRepository;
    
    @Transactional
    public PrestadorDTO criar(PrestadorDTO dto) {
        Prestador prestador = Prestador.builder()
            .nome(dto.getNome())
            .especialidade(dto.getEspecialidade())
            .email(dto.getEmail())
            .telefone(dto.getTelefone())
            .descricao(dto.getDescricao())
            .precoHora(dto.getPrecoHora())
            .ativo(dto.getAtivo() != null ? dto.getAtivo() : true)
            .build();
        
        prestador = prestadorRepository.save(prestador);
        return toDTO(prestador);
    }
    
    public List<PrestadorDTO> listarTodos() {
        return prestadorRepository.findAll()
            .stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }
    
    public List<PrestadorDTO> listarAtivos() {
        return prestadorRepository.findByAtivoTrue()
            .stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }
    
    public PrestadorDTO buscarPorId(Long id) {
        Prestador prestador = prestadorRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Prestador não encontrado"));
        return toDTO(prestador);
    }
    
    @Transactional
    public PrestadorDTO atualizar(Long id, PrestadorDTO dto) {
        Prestador prestador = prestadorRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Prestador não encontrado"));
        
        prestador.setNome(dto.getNome());
        prestador.setEspecialidade(dto.getEspecialidade());
        prestador.setEmail(dto.getEmail());
        prestador.setTelefone(dto.getTelefone());
        prestador.setDescricao(dto.getDescricao());
        prestador.setPrecoHora(dto.getPrecoHora());
        prestador.setAtivo(dto.getAtivo());
        
        prestador = prestadorRepository.save(prestador);
        return toDTO(prestador);
    }
    
    @Transactional
    public void deletar(Long id) {
        Prestador prestador = prestadorRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Prestador não encontrado"));
        prestador.setAtivo(false);
        prestadorRepository.save(prestador);
    }
    
    public List<PrestadorDTO> buscar(String termo) {
        return prestadorRepository
            .findByNomeContainingIgnoreCaseOrEspecialidadeContainingIgnoreCase(termo, termo)
            .stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }
    
    private PrestadorDTO toDTO(Prestador prestador) {
        return PrestadorDTO.builder()
            .id(prestador.getId())
            .nome(prestador.getNome())
            .especialidade(prestador.getEspecialidade())
            .email(prestador.getEmail())
            .telefone(prestador.getTelefone())
            .descricao(prestador.getDescricao())
            .precoHora(prestador.getPrecoHora())
            .ativo(prestador.getAtivo())
            .build();
    }
}