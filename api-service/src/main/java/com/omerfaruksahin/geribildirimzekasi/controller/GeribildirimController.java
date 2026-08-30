package com.omerfaruksahin.geribildirimzekasi.controller;

import com.omerfaruksahin.geribildirimzekasi.entity.Geribildirim;
import com.omerfaruksahin.geribildirimzekasi.service.GeribildirimService;
import jakarta.validation.constraints.NotBlank;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/geribildirimler")
public class GeribildirimController {

    private final GeribildirimService geribildirimService;

    public GeribildirimController(GeribildirimService geribildirimService) {
        this.geribildirimService = geribildirimService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Geribildirim ekle(@RequestBody GeribildirimIstek istek) {
        return geribildirimService.kaydet(istek.metin());
    }

    @GetMapping
    public List<Geribildirim> listele() {
        return geribildirimService.tumunuGetir();
    }

    public record GeribildirimIstek(@NotBlank String metin) {
    }
}
