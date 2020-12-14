package repositories.city;

import entities.CityEntity;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import utils.CreateDummyData;
import utils.InitEntityManager;

import javax.persistence.EntityManager;
import java.util.List;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

public class ICityRepositoryTest {
    private static ICityRepository cityRepository;
    private static EntityManager entityManager;
    private static CityEntity cityEntityForTest;

    @BeforeAll
    public static void setup(){
        cityRepository = new CityRepository(InitEntityManager.initEntityManager());
        entityManager = InitEntityManager.initEntityManager();
        CreateDummyData.createDefaultCities(entityManager);

        cityEntityForTest = new CityEntity();
        cityEntityForTest.setId(UUID.randomUUID());
        cityEntityForTest.setName("BRAILA -1");
        cityEntityForTest.setCountry("Romania -1");
        entityManager.persist(cityEntityForTest);
    }

    @Test
    public void getAll_WhenCalled_ShouldReturn_AllCities(){
        List<CityEntity> cityEntities = entityManager.createQuery("select c from CityEntity c").getResultList();

        assertThat(cityRepository.getAll()).hasSize(cityEntities.size());
    }

    @Test
    public void addCity_WhenCalled_Should_CreateCity(){
        CityEntity cityEntity = new CityEntity();
        cityEntity.setCountry("Romaina");
        cityEntity.setName("BRAILA");
        UUID id = UUID.randomUUID();
        cityEntity.setId(id);

        cityRepository.addCity(cityEntity);

        assertThat(cityRepository.getById(id)).isEqualTo(cityEntity);
    }

    @Test
    public void getCityById_WhenCalled_ShouldReturn_CityEntity(){
        assertThat(cityRepository.getById(cityEntityForTest.getId())).isEqualTo(cityEntityForTest);
    }

    @Test
    public void getCityById_WhenCalled_ShouldReturn_Null(){
        assertThat(cityRepository.getById(UUID.randomUUID())).isEqualTo(null);
    }

    @Test
    public void getCityByName_WhenCalled_ShouldReturn_ListOfCities(){
        List<CityEntity> cityEntities = entityManager.createQuery("select c from CityEntity c where c.name = 'IASI 1'").getResultList();

        assertThat(cityRepository.getByName("IASI 1").size()).isEqualTo(cityEntities.size());
    }

    @Test
    public void getCityByName_WhenCalled_ShouldReturn_EmptyList(){
        assertThat(cityRepository.getByName("IASI 1000").size()).isEqualTo(0);
    }

    @Test
    public void getCityByCountry_WhenCalled_ShouldReturn_ListOfCities(){
        List<CityEntity> cityEntities = entityManager.createQuery("select c from CityEntity c where c.country = 'Romania 1'").getResultList();

        assertThat(cityRepository.getByName("Romania 1").size()).isEqualTo(cityEntities.size());
    }

    @Test
    public void getCityByCountry_WhenCalled_ShouldReturn_EmptyList(){
        assertThat(cityRepository.getByName("Romania 1000").size()).isEqualTo(0);
    }


}