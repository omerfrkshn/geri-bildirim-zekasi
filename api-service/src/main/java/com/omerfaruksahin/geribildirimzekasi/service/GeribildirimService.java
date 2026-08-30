package com.omerfaruksahin.geribildirimzekasi.service;

import com.omerfaruksahin.geribildirimzekasi.client.DuyguAnaliziClient;
import com.omerfaruksahin.geribildirimzekasi.entity.Geribildirim;
import com.omerfaruksahin.geribildirimzekasi.repository.GeribildirimRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class GeribildirimService {

    private final GeribildirimRepository geribildirimRepository;
    private final DuyguAnaliziClient duyguAnaliziClient;

    public GeribildirimService(
            GeribildirimRepository geribildirimRepository,
            DuyguAnaliziClient duyguAnaliziClient) {
        this.geribildirimRepository = geribildirimRepository;
        this.duyguAnaliziClient = duyguAnaliziClient;
    }

    public Geribildirim kaydet(String metin) {
        Geribildirim geribildirim = new Geribildirim(metin);
        duyguAnaliziClient.analizEt(metin).ifPresent(sonuc -> {
            geribildirim.setDuygu(sonuc.duygu());
            geribildirim.setGuven(sonuc.guven());
        });
        return geribildirimRepository.save(geribildirim);
    }

    public List<Geribildirim> tumunuGetir() {
        return geribildirimRepository.findAll();
    }
}
