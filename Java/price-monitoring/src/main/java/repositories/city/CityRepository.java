package repositories.city;

import entities.CityEntity;
import lombok.AllArgsConstructor;

import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import javax.persistence.TypedQuery;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import java.util.List;
import java.util.UUID;

@AllArgsConstructor
public class CityRepository implements ICityRepository {
    private EntityManager entityManager;

    @Override
    public List<CityEntity> getAll() {
        return entityManager.createQuery("select c from CityEntity c").getResultList();
    }

    @Override
    public void addCity(CityEntity cityEntity) {
        EntityTransaction transaction = this.entityManager.getTransaction();
        transaction.begin();
        this.entityManager.persist(cityEntity);
        transaction.commit();
    }

    @Override
    public CityEntity getById(UUID id) {
        return entityManager.find(CityEntity.class, id);
    }

    @Override
    public List<CityEntity> getByName(String name) {
        return entityManager.createQuery("select c from CityEntity c where c.name = :name").setParameter("name", name).getResultList();
    }

    @Override
    public List<CityEntity> getByCountry(String country) {
        return entityManager.createQuery("select c from CityEntity c where c.name = :country").setParameter("country", country).getResultList();
    }
}
