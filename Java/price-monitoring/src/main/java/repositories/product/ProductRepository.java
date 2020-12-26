package repositories.product;

import entities.ProductEntity;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import java.util.List;
import java.util.UUID;

@Named
@ApplicationScoped
public class ProductRepository implements IProductRepository {
    @Inject
    private EntityManager entityManager;

    public List<ProductEntity> demo(){
        return entityManager.createQuery("select p from ProductEntity p").getResultList();
    }

    @Override
    public void add(ProductEntity productEntity) {
        EntityTransaction transaction = this.entityManager.getTransaction();
        try {
            transaction.begin();
            this.entityManager.persist(productEntity);
        } finally {
            transaction.commit();
        }
    }

    @Override
    public ProductEntity getById(UUID id) {
        return entityManager.find(ProductEntity.class, id);
    }

    @Override
    public int getMinYearOfConst() {
        return entityManager.createQuery("select min(p.yearOfConstruction) from ProductEntity p where p.yearOfConstruction > 0").getFirstResult();
    }

    @Override
    public int getMaxYearOfConst() {
        return entityManager.createQuery("select max(p.yearOfConstruction) from ProductEntity p where p.yearOfConstruction > 0").getFirstResult();
    }

    @Override
    public int getMaxNumberOfFloors() {
        return (int) entityManager.createQuery("select max(p.numberOfFloors) from ProductEntity p where p.numberOfFloors > 0").getSingleResult();
    }

    @Override
    public List<Integer> getAllConstructYears() {
        return entityManager.createQuery("select distinct(p.yearOfConstruction) from ProductEntity p " +
                "where p.yearOfConstruction > 0 order by p.yearOfConstruction asc").getResultList();
    }
}
