package repositories.product;

import entities.ProductEntity;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import java.util.UUID;

@Named
@ApplicationScoped
public class ProductRepository implements IProductRepository {
    @Inject
    private EntityManager entityManager;

    @Override
    public void add(ProductEntity productEntity) {
        EntityTransaction transaction = this.entityManager.getTransaction();
        transaction.begin();
        this.entityManager.persist(productEntity);
        transaction.commit();
    }

    @Override
    public ProductEntity getById(UUID id) {
        return entityManager.find(ProductEntity.class, id);
    }
}
