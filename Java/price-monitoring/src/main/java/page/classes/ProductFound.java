package page.classes;

import entities.ProductEntity;
import lombok.Getter;
import lombok.Setter;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.io.IOException;
import java.util.List;
import java.util.Map;

@Named
@RequestScoped
@Getter
@Setter
public class ProductFound {
    private List<ProductEntity> products;

    @PostConstruct
    public void init(){
        Map<String, Object> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getSessionMap();
        products = (List<ProductEntity>) parameterValue.get("products");
    }

    public void evolution(ProductEntity productEntity){
        Map<String, Object> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getSessionMap();
        parameterValue.put("product_for_evaluation", productEntity);
        try {
            FacesContext.getCurrentInstance().getExternalContext().redirect("http://localhost:8080/price_monitoring_war/pages/evolution.xhtml");
        } catch (IOException e) {
        }
    }
}
