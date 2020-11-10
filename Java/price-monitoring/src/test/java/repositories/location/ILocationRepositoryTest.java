package repositories.location;

import entities.CityEntity;
import entities.LocationEntity;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import utils.CreateDummyData;
import utils.InitEntityManager;

import javax.persistence.EntityManager;
import java.util.List;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

class ILocationRepositoryTest {
    private static ILocationRepository locationRepository;
    private static EntityManager entityManager;
    private static LocationEntity locationEntityForTest;

    @BeforeAll
    public static void setup(){
        locationRepository = new LocationRepository(InitEntityManager.initEntityManager());
        entityManager = InitEntityManager.initEntityManager();
        CreateDummyData.createDefaultCities(entityManager);

        locationEntityForTest = new LocationEntity();
        locationEntityForTest.setId(UUID.randomUUID());
        locationEntityForTest.setAddress("Address oras 1");
        locationEntityForTest.setCity(new CityEntity());
        locationEntityForTest.getCity().setId(UUID.randomUUID());

        entityManager.persist(locationEntityForTest);
    }

    @Test
    public void getAll_WhenCalled_ShouldReturn_AllLocations(){
        List<CityEntity> cityEntities = entityManager.createQuery("select l from LocationEntity l").getResultList();

        assertThat(locationRepository.getAll()).hasSize(cityEntities.size());
    }

    @Test
    public void addCity_WhenCalled_Should_CreateCity(){
        CityEntity cityEntity = new CityEntity();
        cityEntity.setCountry("Romaina");
        cityEntity.setName("BRAILA");
        UUID id = UUID.randomUUID();
        cityEntity.setId(id);

//        locationRepository.addCity();

        assertThat(locationRepository.getById(id)).isEqualTo(cityEntity);
    }
}