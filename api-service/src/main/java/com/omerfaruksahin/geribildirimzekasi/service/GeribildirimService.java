package com.omerfaruksahin.geribildirimzekasi.service;

import com.omerfaruksahin.geribildirimzekasi.entity.Geribildirim;
import com.omerfaruksahin.geribildirimzekasi.repository.GeribildirimRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class GeribildirimService {

    private final GeribildirimRepository geribildirimRepository;

    public GeribildirimService(GeribildirimRepository geribildirimRepository) {
        this.geribildirimRepository = geribildirimRepository;
    }

    public Geribildirim kaydet(String metin) {
        Geribildirim geribildirim = new Geribildirim(metin);
        return geribildirimRepository.save(geribildirim);
    }

    public List<Geribildirim> tumunuGetir() {
        return geribildirimRepository.findAll();
    }
}
