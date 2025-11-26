package com.agendamento.controller;

import com.agendamento.dto.PrestadorDTO;
import com.agendamento.service.PrestadorService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/prestadores")
@CrossOrigin(origins = "*")
public class PrestadorController {
    
    @Autowired
    private PrestadorService prestadorService;
    
    @PostMapping
    public ResponseEntity<PrestadorDTO> criar(@Valid @RequestBody PrestadorDTO dto) {
        try {
            PrestadorDTO criado = prestadorService.criar(dto);
            return ResponseEntity.status(HttpStatus.CREATED).body(criado);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
    }
    
    @GetMapping
    public ResponseEntity<List<PrestadorDTO>> listarTodos() {
        List<PrestadorDTO> prestadores = prestadorService.listarTodos();
        return ResponseEntity.ok(prestadores);
    }
    
    @GetMapping("/ativos")
    public ResponseEntity<List<PrestadorDTO>> listarAtivos() {
        List<PrestadorDTO> prestadores = prestadorService.listarAtivos();
        return ResponseEntity.ok(prestadores);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<PrestadorDTO> buscarPorId(@PathVariable Long id) {
        try {
            PrestadorDTO prestador = prestadorService.buscarPorId(id);
            return ResponseEntity.ok(prestador);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<PrestadorDTO> atualizar(
            @PathVariable Long id, 
            @Valid @RequestBody PrestadorDTO dto) {
        try {
            PrestadorDTO atualizado = prestadorService.atualizar(id, dto);
            return ResponseEntity.ok(atualizado);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletar(@PathVariable Long id) {
        try {
            prestadorService.deletar(id);
            return ResponseEntity.noContent().build();
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/buscar")
    public ResponseEntity<List<PrestadorDTO>> buscar(@RequestParam String termo) {
        List<PrestadorDTO> prestadores = prestadorService.buscar(termo);
        return ResponseEntity.ok(prestadores);
    }
}