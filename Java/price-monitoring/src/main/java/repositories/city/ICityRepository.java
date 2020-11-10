package repositories.city;

import entities.CityEntity;

import java.util.List;
import java.util.UUID;

public interface ICityRepository {
    List<CityEntity> getAll();
    void addCity(CityEntity cityEntity);
    CityEntity getById(UUID id);
    List<CityEntity> getByName(String name);
    List<CityEntity> getByCountry(String country);
}
