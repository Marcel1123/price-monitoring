package repositories.product;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;

@Named
@ApplicationScoped
public class ProductPredictionRepository implements IProductPredictionRepository {
    @Inject
    private EntityManager entityManager;

}
