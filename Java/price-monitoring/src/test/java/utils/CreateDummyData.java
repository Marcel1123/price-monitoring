package utils;

import entities.CityEntity;
import entities.LocationEntity;
import repositories.city.ICityRepository;

import javax.persistence.EntityManager;
import java.util.UUID;

public class CreateDummyData {
    public static void createDefaultCities(EntityManager entityManager){
        for(int i = 0; i < 100; i++){
            CityEntity cityEntity = new CityEntity();
            cityEntity.setCountry("Romaina " + i);
            cityEntity.setName("IASI " + i);
            cityEntity.setId(UUID.randomUUID());

            entityManager.persist(cityEntity);

            LocationEntity locationEntity = new LocationEntity();
            locationEntity.setId(UUID.randomUUID());
            locationEntity.setAddress("Adress " + cityEntity.getName() + "  " + cityEntity.getCountry());
            locationEntity.setCity(cityEntity);

            entityManager.persist(locationEntity);
        }
    }
}
